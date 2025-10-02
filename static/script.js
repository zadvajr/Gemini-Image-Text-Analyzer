document.getElementById('analyzer-form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const resultText = document.getElementById('result-text');
    const analyzeBtn = document.getElementById('analyze-btn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const spinner = analyzeBtn.querySelector('.spinner');

    // Show spinner and disable button
    btnText.style.display = 'none';
    spinner.style.display = 'inline-block';
    analyzeBtn.disabled = true;
    resultText.innerHTML = "<em>Analyzing... please wait.</em>";

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Render markdown response
        if (data.text) {
            resultText.innerHTML = marked.parse(data.text);
        } else {
            resultText.innerHTML = `<span style="color: #e74c3c;">${data.error}</span>`;
        }
    } catch (error) {
        resultText.innerHTML = `<span style="color: #e74c3c;">Error: ${error.message}</span>`;
    } finally {
        // Hide spinner and re-enable button
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
        analyzeBtn.disabled = false;
    }
});