const hamburger = document.querySelector('.hamburger');
const navlinks = document.querySelector('.nav-links');
const links = document.querySelectorAll('.nav-links li');
const line_top = document.querySelector('.line1');
const line_bottom = document.querySelector('.line3');
const line_mid = document.querySelector('.line2');

hamburger.addEventListener('click', ()=>{
  navlinks.classList.toggle('open');
  line_top.classList.toggle('rotate');
  line_bottom.classList.toggle('rotate');
  line_mid.classList.toggle('fade');
  
  links.forEach(link =>{
    link.classList.toggle('fade')
  });
});