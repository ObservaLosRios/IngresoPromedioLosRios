// Navegación simple entre secciones (versión limpia sin iframes)
(function(){
  function showSection(sectionId){
    document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
    const target=document.getElementById(sectionId);
    if(target) target.classList.add('active');
    document.querySelectorAll('.nav-link').forEach(l=>l.classList.remove('active'));
    const link=document.querySelector(`.nav-link[data-section="${sectionId}"]`);
    if(link) link.classList.add('active');
    target?.scrollIntoView({behavior:'smooth',block:'start'});
  }

  function initNav(){
    const nav=document.getElementById('nav-links');
    if(!nav) return;
    nav.addEventListener('click', e => {
      const el=e.target;
      if(el && el.classList && el.classList.contains('nav-link')){
        e.preventDefault();
        const section=el.getAttribute('data-section');
        if(section) showSection(section);
      }
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initNav();
    if(!document.querySelector('.section.active')){
      const first=document.querySelector('.section'); if(first) first.classList.add('active');
    }
  });

})();
