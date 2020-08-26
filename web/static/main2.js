// The following code is based off a toggle menu by @Bradcomp
// source: https://gist.github.com/Bradcomp/a9ef2ef322a8e8017443b626208999c1
(function() {
    var burger = document.querySelector('.burger');
    var menu = document.querySelector('#'+burger.dataset.target);
    burger.addEventListener('click', function() {
        burger.classList.toggle('is-active');
        menu.classList.toggle('is-active');
    });
})();
 var $burgers = getAll('.burger');

 if ($burgers.length > 0) {
   $burgers.forEach(function ($el) {
     $el.addEventListener('click', function () {
       var target = $el.dataset.target;
       var $target = document.getElementById(target);
       $el.classList.toggle('is-active');
       $target.classList.toggle('is-active');
     });
   });
 }
const MySUSModal = new SUSModal( {
  id: 'my-bulma-modal',
  animation: "top"
}
);

// for example, display the modal when you click on a button
let btnDisplayModal = document.getElementById("display-modal-bulma")
btnDisplayModal.addEventListener('click', () => {
MySUSModal.show();
}); 