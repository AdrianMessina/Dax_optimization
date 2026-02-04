import { useState } from 'react';
import Editor from '@monaco-editor/react';
import { analyzeDaxCode } from './lib';
import type { DaxAnalysisResult } from './lib';
import './App.css';

const EXAMPLE_DAX = `Total Sales =
SUMX(
    Sales,
    CALCULATE(
        SUMX(
            FILTER(
                Products,
                Products[Category] = "Electronics"
            ),
            Products[Price]
        )
    )
)`;

function App() {
  const [daxCode, setDaxCode] = useState<string>(EXAMPLE_DAX);
  const [analysis, setAnalysis] = useState<DaxAnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    // Simulate async processing
    setTimeout(() => {
      const result = analyzeDaxCode(daxCode);
      setAnalysis(result);
      setIsAnalyzing(false);
    }, 300);
  };

  const handleEditorChange = (value: string | undefined) => {
    if (value !== undefined) {
      setDaxCode(value);
      // Clear analysis when code changes
      if (analysis) {
        setAnalysis(null);
      }
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>⚡ DAX Optimizer</h1>
        <p className="subtitle">Analiza y optimiza tu código DAX para mejor performance</p>
      </header>

      <div className="main-container">
        <div className="editor-section">
          <div className="section-header">
            <h2>Tu código DAX</h2>
            <button
              className="analyze-btn"
              onClick={handleAnalyze}
              disabled={isAnalyzing || !daxCode.trim()}
            >
              {isAnalyzing ? 'Analizando...' : 'Analizar Código'}
            </button>
          </div>
          <div className="editor-wrapper">
            <Editor
              height="500px"
              defaultLanguage="plaintext"
              value={daxCode}
              onChange={handleEditorChange}
              theme="vs-dark"
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                wordWrap: 'on',
                automaticLayout: true,
              }}
            />
          </div>
        </div>

        {analysis && (
          <div className="results-section">
            <div className="score-card">
              <div className="score-circle" style={{
                background: `conic-gradient(${getScoreColor(analysis.score)} ${analysis.score}%, #2a2a2a ${analysis.score}%)`
              }}>
                <div className="score-inner">
                  <span className="score-value">{analysis.score}</span>
                  <span className="score-label">/100</span>
                </div>
              </div>
              <div className="score-info">
                <h3>Puntuación de Performance</h3>
                <p className="object-type">
                  Tipo: <strong>{getObjectTypeLabel(analysis.objectType)}</strong>
                </p>
              </div>
            </div>

            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-label">Complejidad</div>
                <div className="metric-value">{analysis.metrics.complexity}/100</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Iteradores Anidados</div>
                <div className="metric-value">{analysis.metrics.nestedIterators}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Context Transitions</div>
                <div className="metric-value">{analysis.metrics.contextTransitions}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Variables Usadas</div>
                <div className="metric-value">{analysis.metrics.variablesUsed}</div>
              </div>
            </div>

            {analysis.issues.length > 0 && (
              <div className="issues-section">
                <h3>Problemas Detectados ({analysis.issues.length})</h3>
                <div className="issues-list">
                  {analysis.issues.map((issue, index) => (
                    <div key={index} className={`issue-card severity-${issue.severity}`}>
                      <div className="issue-header">
                        <span className={`severity-badge ${issue.severity}`}>
                          {issue.severity === 'critical' ? '🔴' : issue.severity === 'warning' ? '🟡' : 'ℹ️'}
                          {issue.severity.toUpperCase()}
                        </span>
                        <span className="issue-category">{issue.category}</span>
                      </div>
                      <h4>{issue.title}</h4>
                      <p>{issue.description}</p>
                      {issue.snippet && (
                        <pre className="code-snippet">{issue.snippet}</pre>
                      )}
                      {issue.learnMore && (
                        <a href={issue.learnMore} target="_blank" rel="noopener noreferrer" className="learn-more">
                          Aprende más →
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {analysis.suggestions.length > 0 && (
              <div className="suggestions-section">
                <h3>Sugerencias de Optimización ({analysis.suggestions.length})</h3>
                <div className="suggestions-list">
                  {analysis.suggestions.map((suggestion, index) => (
                    <div key={index} className="suggestion-card">
                      <div className="suggestion-header">
                        <h4>{suggestion.title}</h4>
                        <span className={`impact-badge ${suggestion.impact}`}>
                          Impacto: {suggestion.impact === 'high' ? 'Alto' : suggestion.impact === 'medium' ? 'Medio' : 'Bajo'}
                        </span>
                      </div>
                      <p className="suggestion-description">{suggestion.description}</p>
                      <div className="code-comparison">
                        <pre className="suggested-code">{suggestion.suggestedCode}</pre>
                      </div>
                      <p className="suggestion-reason">
                        <strong>Por qué:</strong> {suggestion.reason}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {analysis.issues.length === 0 && (
              <div className="success-message">
                <div className="success-icon">✅</div>
                <h3>¡Excelente trabajo!</h3>
                <p>No se detectaron problemas de performance obvios en tu código DAX.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function getScoreColor(score: number): string {
  if (score >= 80) return '#22c55e';
  if (score >= 60) return '#eab308';
  if (score >= 40) return '#f97316';
  return '#ef4444';
}

function getObjectTypeLabel(type: string): string {
  switch (type) {
    case 'measure':
      return 'Medida';
    case 'calculated-column':
      return 'Columna Calculada';
    case 'calculated-table':
      return 'Tabla Calculada';
    default:
      return type;
  }
}

export default App;
