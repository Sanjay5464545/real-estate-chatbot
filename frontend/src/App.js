import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (query.trim()) {
      // Add user message
      setMessages([...messages, { type: 'user', text: query }]);
      setIsLoading(true);
      
      try {
        // Call Django API
        const response = await axios.post('https://real-estate-chatbot-mxfl.onrender.com/api/analyze/', {

          query: query
        });
        
        if (response.data.success) {
          setMessages(prev => [...prev, { 
            type: 'bot',
            text: response.data.summary,
            chartData: response.data.chart_data,
            tableData: response.data.table_data
          }]);
        } else {
          setMessages(prev => [...prev, { 
            type: 'bot',
            text: '❌ Error: ' + response.data.error
          }]);
        }
      } catch (error) {
        setMessages(prev => [...prev, { 
          type: 'bot',
          text: '❌ Error connecting to backend: ' + error.message
        }]);
      }
      
      setIsLoading(false);
      setQuery('');
    }
  };

  const exampleQueries = [
    "Analyze Wakad",
    "Compare Aundh and Baner",
    "Show price trends for Kharadi"
  ];

  return (
    <div className="App">
      <nav className="navbar navbar-dark bg-gradient shadow-sm">
  <div className="container d-flex justify-content-between align-items-center">
    <span className="navbar-brand mb-0 h1">
      🏠 Real Estate Analysis Chatbot
    </span>
    <div className="d-flex gap-2">
      {messages.length > 0 && (
        <button 
          className="btn btn-sm btn-outline-light"
          onClick={() => setMessages([])}
        >
           Clear Chat
        </button>
      )}
      <span className="badge bg-light text-dark">⚡ Llama 3.3 AI</span>
    </div>
  </div>
</nav>
      <div className="container my-4">
        <div className="row justify-content-center">
          <div className="col-lg-10">
            
            <div className="chat-container shadow-lg">
              
              <div className="messages-area">
                {messages.length === 0 ? (
                  <div className="welcome-screen">
                    <h3>👋 Welcome!</h3>
                    <p className="text-muted">Ask me anything about real estate areas in Pune</p>
                    <div className="example-queries mt-4">
                      <p className="small text-muted mb-2">💡 Try these examples:</p>
                      {exampleQueries.map((ex, idx) => (
                        <button
                          key={idx}
                          className="btn btn-outline-primary btn-sm me-2 mb-2"
                          onClick={() => setQuery(ex)}
                        >
                          {ex}
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.type}`}>
                      <div className="message-avatar">
                        {msg.type === 'user' ? '👤' : '🤖'}
                      </div>
                      <div className="message-content">
                        <div className="message-text">{msg.text}</div>
                        
                        {/* Chart */}
                        {msg.chartData && msg.chartData.labels && msg.chartData.labels.length > 0 && (
                          <div className="chart-container mt-3">
                            <Line
                              data={{
                                labels: msg.chartData.labels,
                                datasets: [{
                                  label: 'Average Price Trend',
                                  data: msg.chartData.values,
                                  borderColor: 'rgb(102, 126, 234)',
                                  backgroundColor: 'rgba(102, 126, 234, 0.1)',
                                  tension: 0.4
                                }]
                              }}
                              options={{
                                responsive: true,
                                plugins: {
                                  legend: { display: true },
                                  title: { display: true, text: 'Price Trends by Year' }
                                }
                              }}
                            />
                          </div>
                        )}
                        
                        {/* Table */}
                        {msg.tableData && msg.tableData.length > 0 && (
                          <div className="table-container mt-3">
                            <div className="table-responsive">
                              <table className="table table-sm table-striped">
                                <thead>
                                  <tr>
                                    {Object.keys(msg.tableData[0]).map((key, i) => (
                                      <th key={i}>{key}</th>
                                    ))}
                                  </tr>
                                </thead>
                                <tbody>
                                  {msg.tableData.slice(0, 10).map((row, i) => (
                                    <tr key={i}>
                                      {Object.values(row).map((val, j) => (
                                        <td key={j}>{val}</td>
                                      ))}
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  ))
                )}
                
                {isLoading && (
                  <div className="message bot">
                    <div className="message-avatar">🤖</div>
                    <div className="message-content">
                      <div className="typing-indicator">
                        <span></span><span></span><span></span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="input-area">
                <form onSubmit={handleSubmit}>
                  <input
                    type="text"
                    className="form-control form-control-lg"
                    placeholder="Type your query... e.g., 'Analyze Wakad'"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    disabled={isLoading}
                  />
                  <button 
                    className="btn btn-primary btn-lg px-4" 
                    type="submit"
                    disabled={isLoading || !query.trim()}
                  >
                    Send 🚀
                  </button>
                </form>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
