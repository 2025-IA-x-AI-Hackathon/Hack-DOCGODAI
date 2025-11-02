interface Course {
  id: number;
  title: string;
  description: string;
  totalSteps: number;
  completedSteps: number;
}

interface Chapter {
  id: number;
  title: string;
  description: string;
  lastStepIndex: number;
}
