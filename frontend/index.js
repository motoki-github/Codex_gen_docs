async function loadIndex() {
  const response = await fetch('../output/index.json');
  return response.json();
}

function App() {
  const [files, setFiles] = React.useState([]);
  const [content, setContent] = React.useState('');

  React.useEffect(() => {
    loadIndex().then(setFiles);
  }, []);

  const loadFile = async (file) => {
    const res = await fetch('../output/' + file);
    const text = await res.text();
    setContent(marked.parse(text));
  };

  return React.createElement('div', null,
    React.createElement('h1', null, 'Generated Docs'),
    React.createElement('ul', null,
      files.map(f => React.createElement('li', {key: f},
        React.createElement('a', {href: '#', onClick: () => loadFile(f)}, f)))
    ),
    React.createElement('div', {dangerouslySetInnerHTML: {__html: content}})
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));

