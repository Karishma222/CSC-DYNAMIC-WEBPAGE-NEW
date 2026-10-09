let index = 0;

function showSlide(num) {
    const slides = document.querySelectorAll(".slide");
    const dots = document.querySelectorAll(".dot");

    if (num >= slides.length) index = 0;
    if (num < 0) index = slides.length - 1;

    slides.forEach(slide => slide.classList.remove("active"));
    dots.forEach(dot => dot.classList.remove("active"));

    slides[index].classList.add("active");
    dots[index].classList.add("active");

    document.querySelector(".slider").style.transform =
        "translateX(" + (-index * 100) + "%)";
}

function autoSlide() {
    index++;
    showSlide(index);
}

setInterval(autoSlide, 3000);

const dots = document.querySelectorAll(".dot");
dots.forEach((dot, i) => {
    dot.addEventListener("click", () => {
        index = i;
        showSlide(index);
    });
});
