document.addEventListener('DOMContentLoaded', function() {
    var menuButton = document.getElementById('menu-button');
    var menu = document.getElementById('menu');

    menuButton.addEventListener('click', function() {
        menu.classList.toggle('closed');
    });
});


      const menuIcon = document.querySelector('.menu-icon');
      const menu = document.querySelector('.menu');

      menuIcon.addEventListener('click', function() {
        menu.classList.toggle('show');
      });

