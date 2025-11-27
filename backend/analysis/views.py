from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import pandas as pd
import os
from groq import Groq

# Initialize Groq client with try-except for Render compatibility
try:
    client = Groq(api_key=settings.GROQ_API_KEY)
except:
    client = None

def get_client():
    global client
    if client is None:
        client = Groq(api_key=settings.GROQ_API_KEY)
    return client

@api_view(['POST'])
def analyze_query(request):
    try:
        query = request.data.get('query', '')
        print(f"📝 Received query: {query}")
        
        # Load Excel data
        excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'real_estate_data.xlsx')
        print(f"📂 Looking for Excel at: {excel_path}")
        
        if not os.path.exists(excel_path):
            return Response({
                'success': False,
                'error': f'Excel file not found. Please place real_estate_data.xlsx in backend folder.'
            }, status=500)
        
        df = pd.read_excel(excel_path)
        print(f"✅ Excel loaded! Columns: {df.columns.tolist()}")
        print(f"📊 Total rows: {len(df)}")
        
        # Find Area/Location column
        area_column = None
        for col in df.columns:
            if 'location' in col.lower() or 'area' in col.lower():
                area_column = col
                break
        
        if area_column is None:
            return Response({
                'success': False,
                'error': f'Could not find location/area column. Available: {df.columns.tolist()}'
            }, status=500)
        
        # Extract areas from query
        query_lower = query.lower()
        areas = df[area_column].unique()
        matched_areas = [area for area in areas if str(area).lower() in query_lower]
        
        # Check if query is just a greeting or invalid
        greetings = ['hello', 'hi', 'hey', 'hii', 'test']
        if any(greet in query_lower for greet in greetings) and not matched_areas:
            return Response({
                'success': True,
                'summary': "👋 Hello! I'm your Real Estate Analysis Assistant powered by Groq's Llama 3.3 AI! Try queries like: 'Analyze Wakad', 'Compare Aundh and Baner', or 'Show price trends for Kharadi'.",
                'chart_data': {'labels': [], 'values': []},
                'table_data': []
            })
        
        # Filter data based on matched areas
        if matched_areas:
            filtered_df = df[df[area_column].isin(matched_areas)]
            print(f"🎯 Matched areas: {matched_areas}, Filtered rows: {len(filtered_df)}")
        else:
            # No match - show sample data
            filtered_df = df.head(15)
            print(f"⚠️ No specific area matched, showing sample data")
        
        # Prepare data summary for LLM
        data_summary = filtered_df.head(5).to_string(index=False)
        
        # Use Groq API with Llama 3.3 model
        summary = ""
        try:
            
            print("🤖 Calling Groq API with Llama 3.3 model...")
            
            chat_completion = get_client().chat.completions.create(

                messages=[
                    {
                        "role": "system",
                        "content": "You are a real estate market analyst. Provide concise, professional analysis in 2-3 sentences focusing on trends, prices, and market insights."
                    },
                    {
                        "role": "user",
                        "content": f"User query: {query}\n\nReal estate data:\n{data_summary}\n\nProvide brief market analysis:"
                    }
                ],
                model="llama-3.3-70b-versatile",  # This is the Llama 3.3 model
                temperature=0.7,
                max_tokens=200
            )
            
            summary = chat_completion.choices[0].message.content
            print("✅ Groq API (Llama 3.3) response received!")
            
        except Exception as llm_error:
            print(f"⚠️ Groq API error: {llm_error}")
            # Fallback summary if Groq fails
            if matched_areas:
                summary = f"📊 Real Estate Analysis for {', '.join(matched_areas)}: Found {len(filtered_df)} property records. The data shows trends in sales, pricing, and market activity across different years."
            else:
                summary = f"📊 Showing sample real estate data with {len(filtered_df)} records. Please specify an area name for detailed analysis."
        
        # Prepare chart data (year-wise price trends)
        chart_data = {'labels': [], 'values': []}
        
        year_col = None
        price_col = None
        
        # Find Year and Price columns
        for col in df.columns:
            col_lower = col.lower()
            if 'year' in col_lower:
                year_col = col
            if 'price' in col_lower or 'sales' in col_lower or 'total_sales' in col_lower:
                price_col = col
        
        if year_col and price_col and len(filtered_df) > 0:
            try:
                yearly_data = filtered_df.groupby(year_col)[price_col].mean().reset_index()
                yearly_data = yearly_data.sort_values(year_col)
                chart_data = {
                    'labels': [str(int(y)) for y in yearly_data[year_col].tolist()],
                    'values': [float(v) for v in yearly_data[price_col].tolist()]
                }
                print(f"📊 Chart data prepared: {len(chart_data['labels'])} data points")
            except Exception as chart_error:
                print(f"⚠️ Chart preparation error: {chart_error}")
        
        # Prepare table data (top 20 records)
        table_data = filtered_df.head(20).fillna('N/A').to_dict('records')
        
        return Response({
            'success': True,
            'summary': summary,
            'chart_data': chart_data,
            'table_data': table_data
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ ERROR: {error_details}")
        
        return Response({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)
