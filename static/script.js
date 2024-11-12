async function fetchResults() {
    const query = document.getElementById('query').value;
    const resultsDiv = document.getElementById('results');
    const loader = document.getElementById('loader');
    resultsDiv.innerHTML = ""; // Clear previous results
    loader.style.display = "block"; // show loader

    if (!query) {
        resultsDiv.innerHTML = "<p>Please enter a search term.</p>";
        loader.style.display = "none"; // hide loader if not query
        return;
    }

    try {
        const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
        const data = await response.json();
        loader.style.display = "none"; // hide loader if search done

        if (data.error) {
            resultsDiv.innerHTML = `<p>${data.error}</p>`;
            return;
        }

        if (data.message) {
            resultsDiv.innerHTML = `<p>${data.message}</p>`;
            return;
        }

        data.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.classList.add('result-item');
            
            resultItem.innerHTML = `
                <h3><a href="${result.link}" target="_blank">${result.title}</a></h3>
                <img src="${result.image_link}" alt="${result.title}" style="width: 250px; height: auto;">
                <p><strong>Published:</strong> ${result.publication_time}</p>
                <p>${result.body_text}</p>
            `;
            resultsDiv.appendChild(resultItem);
        });
    } catch (error) {
        loader.style.display = "none"; // hide loader if error
        resultsDiv.innerHTML = `<p>Failed to fetch results. Please try again later.</p>`;
    }
}