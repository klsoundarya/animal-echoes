// carousel for echoes app
document.addEventListener('DOMContentLoaded', function () {
    
    const funFactsCarousel = document.getElementById('funFactsCarousel');
    const carousel = new bootstrap.Carousel(funFactsCarousel, {
        interval: 3000, 
        ride: 'carousel',
        wrap: true, 
    });

    // Adjust the height of carousel items dynamically
    const carouselItems = document.querySelectorAll('#funFactsCarousel .carousel-item');
    let maxHeight = 0;

    // Find the tallest carousel item
    carouselItems.forEach(item => {
        const height = item.offsetHeight;
        if (height > maxHeight) maxHeight = height;
    });

    // Apply the tallest height to all carousel items
    carouselItems.forEach(item => {
        item.style.minHeight = `${maxHeight}px`;
    });
});
