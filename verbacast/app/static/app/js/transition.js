/* transition   */

window.onload = () => {
    const transition_el = document.querySelector('.transition');
    const anchors = document.querySelectorAll('a');

    setTimeout(() => {
    transition_el.classList.remove('is-active');
    }, 300);

    for (let i = 0; i< anchors.length; i++) {
        const anchor = anchors[i];

        anchor.addEventListener('click', e => {
            e.preventDefault();
            let target = e.target.href;

            transition_el.classList.add('is-active');

            setTimeout(() => {
                window.location.href = target;
            }, 300);
        })
    }
}

document.querySelector('.navbar-brand').addEventListener('click', function(e) {
    e.preventDefault();  // Make sure this is not blocking the default behavior
    // any other code
});





const toggle = document.querySelector('.navbar-toggle');
const links = document.querySelector('.navbar-links');
    
    toggle.addEventListener('click', () => {
        links.classList.toggle('active');
    });

  // Fade out the overlay on page load
  window.addEventListener('load', () => {
    const overlay = document.getElementById('overlay');
    overlay.classList.add('opacity-0');
    setTimeout(() => {
      overlay.style.display = 'none';
    }, 700); // matches transition duration
  });


  