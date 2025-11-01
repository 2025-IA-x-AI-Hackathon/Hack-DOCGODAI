import { heroui } from "@heroui/react";

export default heroui({
  themes: {
    colors: {},
    light: {
      colors: {
        default: {
          DEFAULT: "#e4e4e7",
        },
        primary: {
          DEFAULT: "#14B8A6",
          500: "#14B8A6",
          600: "#12A594",
        },
        secondary: {
          DEFAULT: "#18181b",
        },
        danger: {
          DEFAULT: "#f84d3a",
        },
      },
    },
    dark: {
      colors: {
        default: {
          DEFAULT: "#3f3f46",
        },
        primary: {
          DEFAULT: "#14B8A6",
          500: "#14B8A6",
          600: "#12A594",
        },
        secondary: {
          DEFAULT: "#52525b",
        },
        danger: {
          DEFAULT: "#f84d3a",
        },
      },
    },
  },
});
