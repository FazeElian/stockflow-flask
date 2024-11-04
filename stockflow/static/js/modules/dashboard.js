document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#count').forEach(el => {
        const target = +el.getAttribute('data-target');
        let current = 0;
        const increment = target / 200;

        const updateCount = () => {
            current += increment;
            if (current < target) {
                el.innerText = `$ ${Math.floor(current).toLocaleString()}`;
                requestAnimationFrame(updateCount);
            } else {
                el.innerText = `$ ${target.toLocaleString()}`;
            }
        };

        updateCount();
    });

    document.querySelectorAll('#count2').forEach(el => {
        const target = +el.getAttribute('data-target');
        let current = 0;
        const increment = target / 200;

        const updateCount = () => {
            current += increment;
            if (current < target) {
                el.innerText = `${Math.floor(current).toLocaleString()}`;
                requestAnimationFrame(updateCount);
            } else {
                el.innerText = `${target.toLocaleString()}`;
            }
        };

        updateCount();
    });
});