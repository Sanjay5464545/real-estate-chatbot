from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import pandas as pd
import os
from groq import Groq

# Initialize Groq client once
client = Groq(api_key=settings.GROQ_API_KEY)

@api_view(['POST'])
def analyze_query(request):
    try:
        query = request.data.get('query', '')
        print(f"📝 Received query: {query}")
        
        # Load Excel data
        excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'real_estate_data.xlsx')
        
        if not os.path.exists(excel_path):
            return Response({
                'success': False,
                'error': f'Excel file not found. Please place real_estate_data.xlsx in backend folder.'
            }, status=500)
        
        df = pd.read_excel(excel_path)
        print(f"✅ Excel loaded! Total rows: {len(df)}")
        
        # Find Area/Location column
        area_column = None
        for col in df.columns:
            if 'location' in col.lower() or 'area' in col.lower():
                area_column = col
                break
        
        # Check if query is about real estate or just casual conversation
        query_lower = query.lower()
        real_estate_keywords = ['analyze', 'compare', 'price', 'trend', 'property', 'real estate', 
                                'wakad', 'aundh', 'baner', 'kharadi', 'akurdi', 'demand', 'sales',
                                'show', 'area', 'market', 'pune']
        
        is_real_estate_query = any(keyword in query_lower for keyword in real_estate_keywords)
        
        # Extract areas from query if it's a real estate query
        matched_areas = []
        filtered_df = None
        
        if is_real_estate_query and area_column:
            areas = df[area_column].unique()
            matched_areas = [area for area in areas if str(area).lower() in query_lower]
            
            if matched_areas:
                filtered_df = df[df[area_column].isin(matched_areas)]
                print(f"🎯 Matched areas: {matched_areas}, Filtered rows: {len(filtered_df)}")
            else:
                filtered_df = df.head(15)
                print(f"⚠️ No specific area matched, showing sample data")
        
        # Prepare AI response using Groq
        summary = ""
        
        if is_real_estate_query and filtered_df is not None:
            # REAL ESTATE QUERY - Send data to AI
            data_summary = filtered_df.head(5).to_string(index=False)
            
            print("🤖 Calling Groq AI for real estate analysis...")
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional real estate market analyst. Provide concise, insightful analysis in 2-3 sentences focusing on trends, prices, and market insights."
                    },
                    {
                        "role": "user",
                        "content": f"User query: {query}\n\nReal estate data:\n{data_summary}\n\nProvide brief market analysis:"
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=250
            )
            
            summary = chat_completion.choices[0].message.content
            print("✅ Groq AI real estate analysis complete!")
            
        else:
            # CASUAL CONVERSATION - Let AI respond naturally
            print("💬 Casual conversation detected - using AI for natural response...")
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a friendly Real Estate Analysis Chatbot assistant. When users greet you or ask casual questions, respond warmly and guide them to ask about real estate areas in Pune like Wakad, Aundh, Baner, Kharadi, etc. Keep responses brief (1-2 sentences)."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.9,
                max_tokens=150
            )
            
            summary = chat_completion.choices[0].message.content
            print("✅ Groq AI casual response generated!")
        
        # Prepare chart data only for real estate queries
        chart_data = {'labels': [], 'values': []}
        table_data = []
        
        if is_real_estate_query and filtered_df is not None:
            # Find Year and Price columns
            year_col = None
            price_col = None
            
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
                    print(f"⚠️ Chart error: {chart_error}")
            
            # Prepare table data
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
