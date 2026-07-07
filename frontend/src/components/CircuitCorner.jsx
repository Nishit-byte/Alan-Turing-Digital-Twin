export default function CircuitCorner({ position = 'top-right' }) {
  const flip = position.includes('bottom') ? 'scaleY(-1)' : 'none';
  const flipX = position.includes('left') ? 'scaleX(-1)' : 'none';

  return (
    <svg
      width="140" height="100" viewBox="0 0 140 100"
      style={{
        position: 'absolute',
        [position.includes('top') ? 'top' : 'bottom']: 16,
        [position.includes('left') ? 'left' : 'right']: 16,
        transform: `${flip} ${flipX}`,
        opacity: 0.5,
        pointerEvents: 'none'
      }}
    >
      <path d="M10 10 H70 L85 25 V70" stroke="#e91e8c" strokeWidth="1.5" fill="none" />
      <circle cx="10" cy="10" r="2.5" fill="#e91e8c" />
      <circle cx="85" cy="70" r="2.5" fill="#e91e8c" />
      <path d="M100 90 H130" stroke="#4d7fff" strokeWidth="1.5" fill="none" />
      <circle cx="130" cy="90" r="2" fill="#4d7fff" />
    </svg>
  );
}