export default function GradientWisp() {
  return (
    <svg
      viewBox="0 0 1000 700"
      preserveAspectRatio="none"
      style={{
        position: 'fixed', inset: 0, width: '100%', height: '100%',
        zIndex: 0, opacity: 0.35, pointerEvents: 'none'
      }}
    >
      <defs>
        <linearGradient id="wisp" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#8b3fd1" />
          <stop offset="50%" stopColor="#e91e8c" />
          <stop offset="100%" stopColor="#4d7fff" />
        </linearGradient>
      </defs>
      <path
        d="M-100,600 C150,500 250,750 450,550 C650,350 700,150 1100,50"
        stroke="url(#wisp)" strokeWidth="140" fill="none" strokeLinecap="round"
        opacity="0.6"
      >
        <animate attributeName="d" dur="18s" repeatCount="indefinite"
          values="
            M-100,600 C150,500 250,750 450,550 C650,350 700,150 1100,50;
            M-100,550 C200,650 300,450 500,600 C700,750 750,300 1100,150;
            M-100,600 C150,500 250,750 450,550 C650,350 700,150 1100,50" />
      </path>
    </svg>
  );
}