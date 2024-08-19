//jshint esversion:6

// Change navbar syle when scroll

window.addEventListener ("scroll", () => {
  document.querySelector("nav").classList.toggle('window-scroll', window.scrollY>0)
});


  // show/ hide faq answer
  
  const faqs = document.querySelectorAll(".faq");
  
  faqs.forEach(faq => {
    faq.addEventListener("click", () => {
      // Toggle open class
      faq.classList.toggle("open");
  
      // Toggle icon
      const icon = faq.querySelector('.faq__icon i');
      icon.classList.toggle("uil-minus");
      icon.classList.toggle("uil-plus");
  
      // Close other FAQs
      faqs.forEach(otherFaq => {
        if (otherFaq !== faq) {
          otherFaq.classList.remove("open");
          const otherIcon = otherFaq.querySelector('.faq__icon i');
          otherIcon.classList.remove("uil-minus");
          otherIcon.classList.add("uil-plus");
        }
      });
    });
  });
  
  const menu = document.querySelector(".nav__menu");
  const menuBtn = document.querySelector("#open-menu-btn");
  const closeBtn = document.querySelector("#close-menu-btn");
  
  menuBtn.addEventListener("click", () => {
    menu.style.display = "flex";
    closeBtn.style.display = "inline-block";
    menuBtn.style.display = "none";
  });
  
  closeBtn.addEventListener("click", () => {
    menu.style.display = "none";
    closeBtn.style.display = "none";
    menuBtn.style.display = "inline-block";
  });


//search_bar
const searchBox = document.getElementById('search-box');

searchBox.addEventListener('keyup', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    const query = searchBox.value.trim();
    if (query) {
      const path = `./${query}_imp.html`;
      const url = `${path}`;
      window.location.href = url;
    }
  }
});