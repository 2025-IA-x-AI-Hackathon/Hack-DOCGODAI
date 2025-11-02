import { Button } from "@heroui/react";

import { Card } from "@/shared/ui";

interface Props {
  chapter: Chapter;
}

const getButtonText = (lastStepIndex: number) => {
  if (lastStepIndex === 0) return "시작하기";
  if (lastStepIndex === 3) return "다시보기";
  return "이어하기";
};

const ChapterCard = ({ chapter }: Props) => {
  const progress = Math.round((chapter.lastStepIndex / 3) * 100);

  return (
    <Card className="flex flex-row items-center justify-between gap-8 p-5">
      <div className="flex h-full flex-col justify-start gap-1">
        <div className="line-clamp-1 text-2xl font-semibold">
          {chapter.title}
        </div>
        <div className="text-default-500 line-clamp-2 font-light">
          {chapter.description}
        </div>
      </div>
      <div className="flex items-center gap-4">
        <div className="min-w-10 text-right">
          <div className="text-lg font-bold">{progress}%</div>
          <div className="text-default-500 text-xs">진행률</div>
        </div>
        <Button
          color={chapter.lastStepIndex === 3 ? "secondary" : "primary"}
          radius="full"
        >
          {getButtonText(chapter.lastStepIndex)}
        </Button>
      </div>
    </Card>
  );
};

export default ChapterCard;
