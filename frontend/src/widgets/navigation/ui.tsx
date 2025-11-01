import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
} from "@heroui/react";
import { Link } from "@tanstack/react-router";

import { ThemeSwitcher } from "@/shared/ui";

const Navigation = () => {
  return (
    <Navbar
      classNames={{
        wrapper: "max-w-none px-0",
      }}
    >
      <NavbarBrand>
        <Link to="/">
          <span className="text-primary text-lg font-extrabold tracking-tight md:text-xl">
            POPPINS
          </span>
        </Link>
      </NavbarBrand>
      <NavbarContent justify="end">
        <NavbarItem>
          <Link
            to="/login"
            className="text-default-600 hover:text-foreground text-sm transition-colors"
          >
            로그인
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link
            to="/signup"
            className="text-primary hover:text-primary-600 text-sm font-medium transition-colors"
          >
            회원가입
          </Link>
        </NavbarItem>
        <NavbarItem>
          <ThemeSwitcher />
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
};

export default Navigation;
