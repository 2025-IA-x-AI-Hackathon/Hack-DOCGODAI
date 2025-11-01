import { BookOpenTextIcon, CircleCheckIcon } from "lucide-react";

import CourseCard from "@/pages/dashboard/ui/course-card.tsx";
import NewCourse from "@/pages/dashboard/ui/new-course.tsx";
import { Card, Section } from "@/shared/ui";

const DashboardPage = () => {
  return (
    <Section
      subtitle="진행중인 모든 학습을 한눈에 관리하세요"
      title="내 학습 대시보드"
    >
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <Card className="p-6">
          <div className="text-default-500 text-sm">진행 중</div>
          <div className="text-3xl font-bold">2</div>
        </Card>
        <Card className="p-6">
          <div className="text-default-500 text-sm">완료</div>
          {/*<div className="text-3xl font-bold">{completed.length}</div>*/}
        </Card>
        <Card className="p-6">
          <div className="text-default-500 text-sm">주간 학습(가)</div>
          {/*<div className="text-3xl font-bold">{totalStudyHours}h</div>*/}
        </Card>
        <Card className="p-6">
          <div className="text-default-500 text-sm">평균 정답률</div>
          {/*<div className="text-3xl font-bold">{avgScore}%</div>*/}
        </Card>
      </div>

      <h3 className="mt-10 mb-4 flex items-center gap-2 text-xl font-semibold">
        <BookOpenTextIcon className="text-primary" /> 진행 중 학습
      </h3>
      <div className="grid gap-4 md:grid-cols-2">
        <CourseCard description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris n" />
        <NewCourse />
      </div>

      <h3 className="mt-10 mb-4 flex items-center gap-2 text-xl font-semibold">
        <CircleCheckIcon className="text-primary" />
        완료한 학습
      </h3>
    </Section>
  );
};

export default DashboardPage;
