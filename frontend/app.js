const e = React.createElement;

function App() {
  const [content, setContent] = React.useState('Loading...');

  React.useEffect(() => {
    fetch('../output/index.md')
      .then(res => res.text())
      .then(text => setContent(text))
      .catch(() => setContent('Failed to load documentation.'));
  }, []);

  return e('div', { dangerouslySetInnerHTML: { __html: marked.parse(content) } });
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(e(App));
