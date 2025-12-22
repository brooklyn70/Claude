const http = require('http');

const testOllama = () => {
  const data = JSON.stringify({
    model: 'llama3.2',
    prompt: 'Answer ONLY: SCENE, EPISODE, or OTHER.\n\nText: INT. RESTAURANT - DAY\n\nAnswer:',
    stream: false,
    options: {
      temperature: 0.1,
      num_predict: 10
    }
  });

  const options = {
    hostname: 'ollama.kimacreative.synology.me',
    port: 11434,
    path: '/api/generate',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': data.length
    }
  };

  console.log('🔍 Testing Ollama connection...');
  console.log('URL:', `http://${options.hostname}:${options.port}${options.path}`);

  const req = http.request(options, (res) => {
    let body = '';

    res.on('data', (chunk) => {
      body += chunk;
    });

    res.on('end', () => {
      console.log('\n✅ Response received!');
      console.log('Status:', res.statusCode);
      try {
        const parsed = JSON.parse(body);
        console.log('Response text:', parsed.response);
        console.log('\n✅ Ollama is working correctly!');
      } catch (e) {
        console.log('Raw response:', body.substring(0, 500));
      }
    });
  });

  req.on('error', (error) => {
    console.error('❌ Error:', error.message);
    console.log('\n💡 Tip: Make sure you can access Ollama from n8n Docker network');
  });

  req.setTimeout(30000, () => {
    console.error('❌ Request timeout after 30 seconds');
    req.destroy();
  });

  req.write(data);
  req.end();
};

testOllama();
