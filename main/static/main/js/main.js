// Mobile menu toggle
document.addEventListener('DOMContentLoaded', () => {

    // mobile menu toggle
    const toggle = document.querySelector('.mobile-toggle');
    const nav = document.querySelector('.nav-links');
    if(toggle){
        toggle.addEventListener('click', ()=>{
            nav.style.display = (nav.style.display === 'flex') ? 'none' : 'flex';
            nav.style.flexDirection = 'column';
        });
    }

    // Fade animation
    const fadeElements = document.querySelectorAll('.fade-up');

    function fadeInOnScroll() {
        fadeElements.forEach(el => {
            if (el.getBoundingClientRect().top < window.innerHeight - 50) {
                el.classList.add('visible');
            }
        });
    }

    window.addEventListener('scroll', fadeInOnScroll);
    window.addEventListener('load', fadeInOnScroll);

});


const track = document.querySelector('.carousel-track');
const slides = Array.from(track.children);
const nextButton = document.querySelector('.carousel-btn.right');
const prevButton = document.querySelector('.carousel-btn.left');

let currentIndex = 0;

function updateSlide(index) {
    const cardStyle = getComputedStyle(slides[0]);
    const gap = parseInt(cardStyle.marginRight) || 20; // default gap
    const cardWidth = slides[0].offsetWidth + gap;

    const totalSlides = slides.length;
    const visibleCards = window.innerWidth <= 600 ? 1 :
                         window.innerWidth <= 992 ? 2 : 3;

    if(index < 0) index = totalSlides - visibleCards;
    if(index > totalSlides - visibleCards) index = 0;

    currentIndex = index;

    track.style.transform = `translateX(-${cardWidth * currentIndex}px)`;
}

nextButton.addEventListener('click', () => updateSlide(currentIndex + 1));
prevButton.addEventListener('click', () => updateSlide(currentIndex - 1));

// Optional: auto-slide every 5s
setInterval(() => updateSlide(currentIndex + 1), 5000);

// Recalculate on resize
window.addEventListener('resize', () => updateSlide(currentIndex));


document.addEventListener("scroll", () => {
    document.querySelectorAll(".fade-up").forEach(el => {
        if (el.getBoundingClientRect().top < window.innerHeight - 100) {
            el.classList.add("visible");
        }
    });
});


function toggleMenu() {
    document.getElementById("navLinks").classList.toggle("show");
}

