// Toggle menu on mobile
document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.getElementById('menu-toggle');
  const navLinks = document.querySelector('.nav-links');

  toggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
  });
});
// for community section
const track = document.querySelector('.slider-track');
const images = document.querySelectorAll('.slider-track img');
const btnLeft = document.querySelector('.slider-btn.left');
const btnRight = document.querySelector('.slider-btn.right');

let currentIndex = 0;

btnLeft.addEventListener('click', () => {
  if (currentIndex > 0) {
    currentIndex--;
    updateSlider();
  }
});

btnRight.addEventListener('click', () => {
  if (currentIndex < images.length - 1) {
    currentIndex++;
    updateSlider();
  }
});

function updateSlider() {
  const slideWidth = images[0].clientWidth;
  track.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
}
