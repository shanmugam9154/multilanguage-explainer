/**
 * Frontend logic for the Multilingual Learning Assistant.
 * Handles API communication and DOM manipulation.
 */

const API_BASE_URL = "http://localhost:5000/api";

// DOM Elements
const outputDiv = document.getElementById('output');
const topicInput = document.getElementById('topic');
const languageSelect = document.getElementById('language');
const gradeSelect = document.getElementById('grade');

/**
 * Main handler for all API actions
 * @param {string} endpoint - The API endpoint to call ('explain', 'summary', or 'quiz')
 */
async function handleRequest(endpoint) {
    const topic = topicInput.value.trim();
    const language = languageSelect.value;
    const grade = gradeSelect.value;

    // Validation: Topics are required for explain and quiz
    if (!topic && endpoint !== 'summary') {
        showError("Please enter a topic first.");
        return;
    }

    // Prepare payload
    const payload = { language };
    
    if (endpoint === 'explain') {
        payload.topic = topic;
        payload.grade = grade;
    } else if (endpoint === 'quiz') {
        payload.topic = topic;
    } else if (endpoint === 'summary') {
        // Summarizes whatever text is currently in the output area
        const currentContent = outputDiv.innerText;
        if (!currentContent || currentContent.includes("Results will appear here")) {
            showError("No text found in output to summarize.");
            return;
        }
        payload.text = currentContent;
    }

    setLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to fetch data from AI.");
        }

        renderOutput(endpoint, data);
    } catch (err) {
        showError(err.message);
    } finally {
        setLoading(false);
    }
}

/**
 * Renders the structured JSON response into HTML
 */
function renderOutput(type, data) {
    outputDiv.innerHTML = ""; // Clear current content

    if (type === 'explain') {
        outputDiv.innerHTML = `
            <div class="result-card">
                <h2 style="color: #2563eb;">${data.title || 'Explanation'}</h2>
                <div class="content">${data.explanation}</div>
                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
                <p><strong>Key Vocabulary:</strong> ${data.key_terms ? data.key_terms.join(', ') : 'N/A'}</p>
            </div>
        `;
    } 
    else if (type === 'summary') {
        const bullets = data.bullet_points?.map(p => `<li>${p}</li>`).join('') || '';
        outputDiv.innerHTML = `
            <div class="result-card">
                <h2>Summary</h2>
                <p><em>${data.summary}</em></p>
                <ul>${bullets}</ul>
            </div>
        `;
    } 
    else if (type === 'quiz') {
        const quizHtml = data.quiz.map((q, i) => `
            <div style="margin-bottom: 20px; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px;">
                <p><strong>Q${i + 1}: ${q.question}</strong></p>
                ${q.options.map(opt => `<label style="display:block;"><input type="radio" disabled> ${opt}</label>`).join('')}
                <details style="margin-top: 8px; cursor: pointer; color: #059669;">
                    <summary>Show Correct Answer</summary>
                    <p style="padding-left: 10px; font-weight: bold;">✅ ${q.correct_answer}</p>
                </details>
            </div>
        `).join('');
        outputDiv.innerHTML = `<h2>Quiz</h2>${quizHtml}`;
    }
}

function setLoading(isLoading) {
    outputDiv.innerHTML = isLoading ? '<p class="loading">Generating AI response...</p>' : '';
}

function showError(msg) {
    outputDiv.innerHTML = `<div class="error"><strong>Error:</strong> ${msg}</div>`;
}