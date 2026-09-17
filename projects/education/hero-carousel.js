const heroSlides = [
  {
    image: 'assets/campus-hero.png',
    eyebrow: 'STUDENT ADMINISTRATION',
    title: 'Enrollment, records<br>and student support',
    text: 'Register students, review academic progress and record follow-up work.',
    credit: 'Campus image'
  },
  {
    image: 'assets/ub-student-centre.jpg',
    eyebrow: 'ACADEMIC RECORDS',
    title: 'Review attendance<br>and academic progress',
    text: 'Use the student record to check grades, failed courses, warnings and attendance.',
    credit: 'University of Botswana central campus · CNJerem · CC BY 4.0'
  },
  {
    image: 'assets/ub-administration.jpg',
    eyebrow: 'STUDENT SUPPORT',
    title: 'Record each action<br>and follow-up date',
    text: 'Keep calls, meetings, referrals and outcomes attached to the student record.',
    credit: 'University of Botswana administration building · Iulus Ascanius · Public domain'
  }
];

const hero = document.querySelector('.software-site .hero');
let heroIndex = 0;
let heroTimer;

function showHeroSlide(index) {
  heroIndex = (index + heroSlides.length) % heroSlides.length;
  const slide = heroSlides[heroIndex];
  hero.classList.add('changing');
  window.setTimeout(() => {
    hero.style.backgroundImage = `linear-gradient(90deg,rgba(4,16,28,.82),rgba(4,16,28,.16)),url('${slide.image}')`;
    heroEyebrow.textContent = slide.eyebrow;
    heroTitle.innerHTML = slide.title;
    heroText.textContent = slide.text;
    heroCredit.textContent = slide.credit;
    [...heroDots.children].forEach((dot, i) => dot.classList.toggle('active', i === heroIndex));
    hero.classList.remove('changing');
  }, 170);
}

function restartHeroTimer() {
  window.clearInterval(heroTimer);
  heroTimer = window.setInterval(() => showHeroSlide(heroIndex + 1), 7000);
}

heroSlides.forEach((_, index) => {
  const dot = document.createElement('button');
  dot.setAttribute('aria-label', `Show slide ${index + 1}`);
  dot.addEventListener('click', () => { showHeroSlide(index); restartHeroTimer(); });
  heroDots.append(dot);
});
heroPrev.addEventListener('click', () => { showHeroSlide(heroIndex - 1); restartHeroTimer(); });
heroNext.addEventListener('click', () => { showHeroSlide(heroIndex + 1); restartHeroTimer(); });
hero.addEventListener('mouseenter', () => window.clearInterval(heroTimer));
hero.addEventListener('mouseleave', restartHeroTimer);
document.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft') heroPrev.click();
  if (event.key === 'ArrowRight') heroNext.click();
});
showHeroSlide(0);
restartHeroTimer();
