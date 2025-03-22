document.getElementById('ingest-btn').addEventListener('click', function() {
    const url = document.getElementById('url').value;
    const loading = document.getElementById('loading');
    loading.style.display = 'block';

    fetch(`/scrape?url=${encodeURIComponent(url)}`)
        .then(response => response.json())
        .then(data => {
            if (data.content) {
                loading.style.display = 'none';
                localStorage.setItem('content', data.content); // Save content in localStorage for later use
                alert('Content ingested successfully!');
            } else {
                loading.style.display = 'none';
                alert('Failed to ingest content!');
            }
        })
        .catch(error => {
            loading.style.display = 'none';
            alert('Error: ' + error);
        });
});

document.getElementById('ask-btn').addEventListener('click', function() {
    const url = document.getElementById('url').value;
    const question = document.getElementById('question').value;
    const content = localStorage.getItem('content'); // Retrieve the saved content from localStorage
    const loading = document.getElementById('loading');
    loading.style.display = 'block';

    if (!content) {
        loading.style.display = 'none';
        alert('Please ingest content first by providing a URL!');
        return;
    }

    fetch(`/ask?url=${encodeURIComponent(url)}&question=${encodeURIComponent(question)}`)
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            if (data.answer) {
                document.getElementById('answer').textContent = `Answer: ${data.answer}`;
            } else {
                document.getElementById('answer').textContent = 'No answer found.';
            }
        })
        .catch(error => {
            loading.style.display = 'none';
            alert('Error: ' + error);
        });
});
