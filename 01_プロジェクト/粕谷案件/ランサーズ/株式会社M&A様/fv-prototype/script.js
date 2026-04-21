document.addEventListener('DOMContentLoaded', () => {
  // スクロールアニメーションの監視
  const fadeElements = document.querySelectorAll('.js-scroll-anim');

  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -10% 0px', // 画面の下から10%のラインを超えたら発火
    threshold: 0
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-active');
        // 一度発火したら監視を解除する場合
        obs.unobserve(entry.target);
      }
    });
  }, observerOptions);

  fadeElements.forEach(el => {
    observer.observe(el);
  });

  // ハンバーガーメニューのトグル処理
  const hamburger = document.querySelector('.js-hamburger');
  const closeBtn = document.querySelector('.js-mobile-close');
  const mobileMenu = document.querySelector('.js-mobile-menu');
  const menuLinks = document.querySelectorAll('.js-menu-link');

  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('is-active');
      mobileMenu.classList.toggle('is-active');
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        hamburger.classList.remove('is-active');
        mobileMenu.classList.remove('is-active');
      });
    }

    // リンククリック時にメニューを閉じる
    menuLinks.forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('is-active');
        mobileMenu.classList.remove('is-active');
      });
    });
  }
});
