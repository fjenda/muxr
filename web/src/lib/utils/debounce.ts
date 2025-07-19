/**
 * Creates a debounce function that delays the execution of the provided function
 * @param delay - The delay in milliseconds before the function is executed
 */
export const createDebounce = (delay: number): (func: () => void) => void => {
    let timeout: ReturnType<typeof setTimeout> | undefined;

    return (func: () => void) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            timeout = undefined;
            func();
        }, delay);
    };
}