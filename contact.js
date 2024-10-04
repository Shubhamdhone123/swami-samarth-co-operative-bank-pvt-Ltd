document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Your Problem will be solved as soon as possible');
    
    this.reset();
});
