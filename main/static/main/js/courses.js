document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('courseSearch');
    const button = document.getElementById('searchButton');
    const cards = document.querySelectorAll('.course-card');
    const grid = document.querySelector('.course-grid');

    if (!input || !grid) return;

    const noResult = document.createElement('div');
    noResult.className = 'no-courses';
    noResult.style.display = 'none';
    noResult.innerHTML = '<h3>No courses found.</h3><p>Vera keyword try pannunga.</p>';
    grid.appendChild(noResult);

    function searchCourses() {
        const query = input.value.trim().toLowerCase();
        let visible = 0;

        cards.forEach(function (card) {
            const name = (card.dataset.course || '').toLowerCase();
            const p = card.querySelector('p');
            const desc = p ? p.textContent.toLowerCase() : '';
            const match = name.includes(query) || desc.includes(query);

            card.style.display = match ? 'block' : 'none';
            if (match) visible++;
        });

        noResult.style.display = (visible === 0 && cards.length > 0) ? 'block' : 'none';
    }

    input.addEventListener('input', searchCourses);
    button.addEventListener('click', function () {
        searchCourses();
        const section = document.querySelector('.courses-section');
        if (section) section.scrollIntoView({ behavior: 'smooth' });
    });
    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            button.click();
        }
    });
});