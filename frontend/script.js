const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Initialize Mermaid
mermaid.initialize({ startOnLoad: false, theme: 'dark' });

// Auto-resize textarea
userInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Handle Enter key
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

// Quick Action Buttons
document.querySelectorAll('.quick-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const prompt = btn.getAttribute('data-prompt');
        userInput.value = prompt;
        sendMessage();
    });
});

async function sendMessage() {
    const text = userInput.value.trim();
    const datasetContext = document.getElementById('dataset-context').value.trim();

    if (!text) return;

    // Add User Message
    addMessage(text, 'user');
    userInput.value = '';
    userInput.style.height = 'auto';

    // Show Loading State (Optional: Add a typing indicator here)
    const loadingId = addMessage('Thinking...', 'ai', true);

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: text,
                dataset_context: datasetContext
            }),
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();

        // Remove loading message and add actual response
        removeMessage(loadingId);
        addMessage(data.response, 'ai');

    } catch (error) {
        removeMessage(loadingId);
        addMessage('Sorry, something went wrong. Please try again.', 'ai');
        console.error('Error:', error);
    }
}

function addMessage(text, sender, isLoading = false) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}-message`;
    if (isLoading) msgDiv.id = 'loading-msg';

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = sender === 'ai' ? 'AI' : 'You';

    const content = document.createElement('div');
    content.className = 'content';

    if (sender === 'ai' && !isLoading) {
        // Parse Markdown
        content.innerHTML = marked.parse(text);

        // Render Math with KaTeX
        renderMathInElement(content, {
            delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false }
            ],
            throwOnError: false
        });

        // Render Mermaid Diagrams
        content.querySelectorAll('.language-mermaid').forEach((block) => {
            const graphDefinition = block.textContent;
            const id = `mermaid-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
            const mermaidDiv = document.createElement('div');
            mermaidDiv.id = id;
            mermaidDiv.className = 'mermaid';
            block.parentElement.replaceWith(mermaidDiv);

            mermaid.render(id, graphDefinition).then(({ svg }) => {
                mermaidDiv.innerHTML = svg;
            });
        });

        // Highlight Code
        content.querySelectorAll('pre code').forEach((block) => {
            if (!block.classList.contains('language-mermaid')) {
                hljs.highlightElement(block);
            }
        });
    } else {
        content.textContent = text;
    }

    msgDiv.appendChild(avatar);
    msgDiv.appendChild(content);
    chatContainer.appendChild(msgDiv);

    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;

    return msgDiv.id; // Return ID if needed
}

function removeMessage(id) {
    const msg = document.getElementById('loading-msg');
    if (msg) msg.remove();
}
