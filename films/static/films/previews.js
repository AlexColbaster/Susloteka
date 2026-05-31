document.addEventListener('DOMContentLoaded', () => {
  const previews = document.querySelectorAll('[data-video-preview]');

  const captureFrame = (img) => {
    const src = img.dataset.videoSrc;
    if (!src) return;

    const video = document.createElement('video');
    video.src = src;
    video.crossOrigin = 'anonymous';
    video.muted = true;
    video.playsInline = true;
    video.preload = 'metadata';

    const cleanup = () => {
      video.removeAttribute('src');
      video.load();
    };

    video.addEventListener('loadedmetadata', () => {
      if (!Number.isFinite(video.duration) || video.duration <= 0) {
        cleanup();
        return;
      }

      const min = video.duration * 0.1;
      const max = video.duration * 0.85;
      const time = Math.max(0.01, min + Math.random() * Math.max(0.01, max - min));
      video.currentTime = time;
    }, { once: true });

    video.addEventListener('seeked', () => {
      const width = video.videoWidth || 1280;
      const height = video.videoHeight || 720;
      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      const context = canvas.getContext('2d');

      if (!context) {
        cleanup();
        return;
      }

      context.drawImage(video, 0, 0, width, height);
      img.src = canvas.toDataURL('image/jpeg', 0.82);
      cleanup();
    }, { once: true });

    video.addEventListener('error', cleanup, { once: true });
  };

  previews.forEach((img) => captureFrame(img));
});
