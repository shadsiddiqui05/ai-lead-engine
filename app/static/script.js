document.getElementById('leadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const btn = document.getElementById('submitBtn');
    const statusDiv = document.getElementById('statusMessage');
    
    // Set loading state
    btn.classList.add('loading');
    btn.disabled = true;
    statusDiv.className = 'status-message';
    
    const payload = {
        prospect_name: document.getElementById('prospect_name').value,
        email: document.getElementById('email').value,
        company_name: document.getElementById('company_name').value,
        website: document.getElementById('website').value
    };

    try {
        const response = await fetch('/api/v1/leads', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            statusDiv.innerHTML = `✅ <strong>Success!</strong><br/>${data.message}`;
            statusDiv.className = 'status-message status-success';
            document.getElementById('leadForm').reset();
        } else {
            statusDiv.innerHTML = `❌ <strong>Error:</strong><br/>${data.detail || 'An unknown error occurred.'}`;
            statusDiv.className = 'status-message status-error';
        }
    } catch (error) {
        statusDiv.innerHTML = `❌ <strong>Network Error:</strong><br/>Could not connect to the server.`;
        statusDiv.className = 'status-message status-error';
    } finally {
        // Reset button state
        btn.classList.remove('loading');
        btn.disabled = false;
    }
});
