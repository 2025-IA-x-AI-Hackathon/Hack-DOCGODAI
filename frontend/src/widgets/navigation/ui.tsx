import { Navbar, NavbarBrand, NavbarContent, NavbarItem } from "@heroui/react";

import { ThemeSwitcher } from "@/shared/ui";

const Navigation = () => {
  return (
    <Navbar
      classNames={{
        wrapper: "max-w-none px-0",
      }}
    >
      <NavbarBrand>
        <span className="text-primary text-lg font-extrabold tracking-tight md:text-xl">
          POPPINS
        </span>
      </NavbarBrand>
      <NavbarContent justify="end">
        <NavbarItem>
          <ThemeSwitcher />
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
};

export default Navigation;
