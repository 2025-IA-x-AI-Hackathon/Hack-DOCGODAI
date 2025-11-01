import { Button, Form } from "@heroui/react";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link } from "@tanstack/react-router";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { ROUTE } from "@/shared/constants";
import { formStyle } from "@/shared/styles";
import { HookFormInput, Section } from "@/shared/ui";

const loginSchema = z.object({
  email: z
    .string()
    .min(1, "이메일을 입력해주세요")
    .email("올바른 이메일 형식을 입력해주세요"),
  password: z
    .string()
    .min(8, "비밀번호는 최소 8자 이상이어야 합니다")
    .max(20, "비밀번호는 최대 20자 이하이어야 합니다"),
});

type LoginFormData = z.infer<typeof loginSchema>;

const LoginPage = () => {
  const {
    control,
    handleSubmit,
    formState: { isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    // TODO: 실제 로그인 API 호출
    console.log("Login data:", data);
    await new Promise((resolve) => setTimeout(resolve, 1000));
  };

  const styles = formStyle();

  return (
    <Section>
      <div className={styles.wrapper()}>
        <div className="flex flex-col gap-2 text-center">
          <h1 className={styles.title()}>로그인</h1>
          <p className="text-default-500 text-sm">
            계정에 로그인하여 학습을 시작하세요
          </p>
        </div>

        <Form className={styles.form()} onSubmit={handleSubmit(onSubmit)}>
          <HookFormInput
            control={control}
            label="이메일"
            name="email"
            type="email"
          />

          <HookFormInput
            control={control}
            label="비밀번호"
            name="password"
            type="password"
          />

          <Button
            className="w-full"
            color="primary"
            isLoading={isSubmitting}
            type="submit"
          >
            로그인
          </Button>
        </Form>

        <div className="text-center text-sm">
          <p className="text-default-500">
            계정이 없으신가요?{" "}
            <Link className="text-primary hover:underline" to={ROUTE.signup}>
              회원가입
            </Link>
          </p>
        </div>
      </div>
    </Section>
  );
};

export default LoginPage;
