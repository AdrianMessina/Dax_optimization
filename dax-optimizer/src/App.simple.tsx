import { useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="app">
      <header className="app-header">
        <h1>⚡ DAX Optimizer - Test Simple</h1>
        <p className="subtitle">Si ves esto, React está funcionando</p>
      </header>

      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h2>Contador de prueba: {count}</h2>
        <button
          onClick={() => setCount(count + 1)}
          style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}
        >
          Incrementar
        </button>
      </div>
    </div>
  );
}

export default App;
