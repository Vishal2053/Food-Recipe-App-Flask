document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const input = document.querySelector('input[type="text"]');
    
    form.addEventListener('submit', () => {
        if (!input.value.trim()) {
            alert('Please enter a recipe name!');
        }
    });
});
