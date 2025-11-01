import { Button, Form } from "@heroui/react";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link } from "@tanstack/react-router";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { formStyle } from "@/shared/styles";
import { HookFormInput, Section } from "@/shared/ui";

const signupSchema = z.object({
  name: z.string().min(1, "이름을 입력해주세요"),
  email: z.string().email("올바른 이메일 형식을 입력해주세요"),
  password: z
    .string()
    .min(8, "비밀번호는 최소 8자 이상이어야 합니다")
    .max(20, "비밀번호는 최대 20자 이하이어야 합니다"),
});

type SignupFormData = z.infer<typeof signupSchema>;

const SignupPage = () => {
  const {
    control,
    handleSubmit,
    formState: { isSubmitting, isValid },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
    mode: "onBlur",
    defaultValues: {
      name: "",
      email: "",
      password: "",
    },
  });

  const onSubmit = async (data: SignupFormData) => {
    // TODO: 실제 회원가입 API 호출
    console.log("Signup data:", data);
    await new Promise((resolve) => setTimeout(resolve, 1000));
  };

  const styles = formStyle();

  return (
    <Section>
      <div className={styles.wrapper()}>
        <div className="text-center">
          <h1 className={styles.title()}>회원가입</h1>
          <p className="text-default-500 mt-2 text-sm">
            새 계정을 만들어 학습을 시작하세요
          </p>
        </div>

        <Form className={styles.form()} onSubmit={handleSubmit(onSubmit)}>
          <HookFormInput
            isRequired
            control={control}
            label="이름"
            name="name"
            type="text"
          />

          <HookFormInput
            isRequired
            control={control}
            label="이메일"
            name="email"
            type="email"
          />

          <HookFormInput
            isRequired
            control={control}
            description="8자 이상 20자 이하의 비밀번호를 입력해주세요"
            label="비밀번호"
            name="password"
            type="password"
          />

          <Button
            className="w-full"
            color="primary"
            isDisabled={!isValid}
            isLoading={isSubmitting}
            type="submit"
          >
            회원가입
          </Button>
        </Form>

        <div className="text-center text-sm">
          <p className="text-default-500">
            이미 계정이 있으신가요?{" "}
            <Link className="text-primary hover:underline" to="/login">
              로그인
            </Link>
          </p>
        </div>
      </div>
    </Section>
  );
};

export default SignupPage;
