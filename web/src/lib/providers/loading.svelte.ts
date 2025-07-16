export const loading = $state({
    visible: false,
    message: 'Loading...',
});

export const LoadingActions = {
    show: (message: string = 'Loading...') => {
        loading.visible = true;
        loading.message = message;
    },
    hide: () => {
        loading.visible = false;
    },
    wrap: async <T>(promise: Promise<T>, message?: string): Promise<T> => {
        LoadingActions.show(message);
        try {
            return await promise;
        } finally {
            LoadingActions.hide();
        }
    }
};
