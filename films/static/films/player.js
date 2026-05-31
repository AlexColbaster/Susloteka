document.addEventListener('DOMContentLoaded', () => {
  const video = document.querySelector('#film-video');
  const player = document.querySelector('.video-player');
  const overlay = document.querySelector('[data-video-play]');
  const toggle = document.querySelector('[data-video-toggle]');
  const toggleIcon = document.querySelector('[data-video-toggle-icon]');
  const fullscreen = document.querySelector('[data-video-fullscreen]');
  const fullscreenIcon = document.querySelector('[data-video-fullscreen-icon]');
  const progress = document.querySelector('[data-video-progress]');
  const time = document.querySelector('[data-video-time]');

  if (!video || !player || !overlay || !toggle || !toggleIcon || !fullscreen || !fullscreenIcon || !progress || !time) {
    return;
  }

  const formatTime = (seconds) => {
    if (!Number.isFinite(seconds)) return '0:00';
    const total = Math.max(0, Math.floor(seconds));
    const mins = Math.floor(total / 60);
    const secs = String(total % 60).padStart(2, '0');
    return `${mins}:${secs}`;
  };

  const syncUI = () => {
    const duration = video.duration || 0;
    const current = video.currentTime || 0;
    progress.value = duration ? Math.round((current / duration) * 1000) : 0;
    time.textContent = `${formatTime(current)} / ${formatTime(duration)}`;
    toggleIcon.textContent = video.paused ? '▶' : '❚❚';
    fullscreenIcon.textContent = document.fullscreenElement ? '⤢' : '⛶';
    overlay.classList.toggle('is-hidden', !video.paused || current > 0);
  };

  overlay.addEventListener('click', async () => {
    await video.play();
    syncUI();
  });

  toggle.addEventListener('click', async () => {
    if (video.paused) {
      await video.play();
    } else {
      video.pause();
    }
    syncUI();
  });

  fullscreen.addEventListener('click', async () => {
    if (document.fullscreenElement) {
      await document.exitFullscreen();
    } else if (player.requestFullscreen) {
      await player.requestFullscreen();
    }
    syncUI();
  });

  progress.addEventListener('input', () => {
    if (!video.duration) return;
    video.currentTime = (Number(progress.value) / 1000) * video.duration;
  });

  video.addEventListener('loadedmetadata', syncUI);
  video.addEventListener('timeupdate', syncUI);
  video.addEventListener('play', syncUI);
  video.addEventListener('pause', syncUI);
  document.addEventListener('fullscreenchange', syncUI);
  video.addEventListener('ended', () => {
    overlay.classList.remove('is-hidden');
    toggleIcon.textContent = '▶';
    progress.value = 0;
    time.textContent = `0:00 / ${formatTime(video.duration || 0)}`;
    fullscreenIcon.textContent = document.fullscreenElement ? '⤢' : '⛶';
  });
});
