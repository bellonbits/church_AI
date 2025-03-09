document.addEventListener('DOMContentLoaded', function() {
    // Quiet Time Form
    document.getElementById('quiet-time-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const duration = document.getElementById('duration').value;
        const focusArea = document.getElementById('focus-area').value;
        
        document.getElementById('quiet-time-result').classList.add('d-none');
        document.getElementById('quiet-time-content').innerHTML = 'Loading...';
        document.getElementById('quiet-time-result').classList.remove('d-none');
        
        try {
            const response = await fetch('/quiet-time', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    duration: parseInt(duration),
                    focus_area: focusArea || null
                })
            });
            
            const data = await response.json();
            document.getElementById('quiet-time-content').innerHTML = data.result.replace(/\\n/g, '<br>');
        } catch (error) {
            document.getElementById('quiet-time-content').innerHTML = 'Error: ' + error.message;
        }
    });
    
    // Books Form
    document.getElementById('books-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const topic = document.getElementById('topic').value;
        const spiritualLevel = document.getElementById('spiritual-level').value;
        const count = document.getElementById('count').value;
        
        document.getElementById('books-result').classList.add('d-none');
        document.getElementById('books-content').innerHTML = 'Loading...';
        document.getElementById('books-result').classList.remove('d-none');
        
        try {
            const response = await fetch('/recommend-books', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    topic: topic || null,
                    spiritual_level: spiritualLevel,
                    count: parseInt(count)
                })
            });
            
            const data = await response.json();
            document.getElementById('books-content').innerHTML = data.result.replace(/\\n/g, '<br>');
        } catch (error) {
            document.getElementById('books-content').innerHTML = 'Error: ' + error.message;
        }
    });
    
    // Bible Study Form
    document.getElementById('bible-study-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const passage = document.getElementById('passage').value;
        
        document.getElementById('bible-study-result').classList.add('d-none');
        document.getElementById('bible-study-content').innerHTML = 'Loading...';
        document.getElementById('bible-study-result').classList.remove('d-none');
        
        try {
            const response = await fetch('/bible-study', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    passage: passage
                })
            });
            
            const data = await response.json();
            document.getElementById('bible-study-content').innerHTML = data.result.replace(/\\n/g, '<br>');
        } catch (error) {
            document.getElementById('bible-study-content').innerHTML = 'Error: ' + error.message;
        }
    });
    
    // Question Form
    document.getElementById('question-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const question = document.getElementById('question').value;
        
        document.getElementById('question-result').classList.add('d-none');
        document.getElementById('question-content').innerHTML = 'Loading...';
        document.getElementById('question-result').classList.remove('d-none');
        
        try {
            const response = await fetch('/answer-question', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    question: question
                })
            });
            
            const data = await response.json();
            document.getElementById('question-content').innerHTML = data.result.replace(/\\n/g, '<br>');
        } catch (error) {
            document.getElementById('question-content').innerHTML = 'Error: ' + error.message;
        }
    });
});