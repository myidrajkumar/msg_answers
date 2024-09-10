function submitQuestion() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value;
    if (!question) return;

    addMessage('user-message', question);
    showLoading(true);

    questionInput.value = '';

    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        addMessage('bot-message', data.content);
    })
    .catch(error => {
        showLoading(false);
        addMessage('bot-message', 'An error occurred. Please try again.');
        console.error('Error:', error);
    });
}

function addMessage(className, message) {
    console.log('Adding message:', className, message);
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = message;
    
    messageDiv.appendChild(bubble);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; 
}

function showLoading(isLoading) {
    const loading = document.getElementById('loading');
    if (isLoading) {
        loading.classList.remove('d-none');
    } else {
        loading.classList.add('d-none');
    }
}
