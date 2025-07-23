export const processingState = $state({
    filename: "" as string,
    percentage: 0 as number,
    status: "Idle" as string,
    sessionId: null as string | null,
});