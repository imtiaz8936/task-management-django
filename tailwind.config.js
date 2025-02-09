/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Template at the project level
    "./**/templates/**/*.html", // Tempalate inside Apps
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

