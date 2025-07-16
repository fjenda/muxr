export const trackUrls = $state({
    urls: [] as string[],
    addUrl: (url: string) => {
        if (!trackUrls.urls.includes(url)) {
            trackUrls.urls.push(url);
        }
    },
    removeUrl: (url: string) => {
        const index = trackUrls.urls.indexOf(url);
        if (index !== -1) {
            trackUrls.urls.splice(index, 1);
        }
    },
    clear: () => {
        trackUrls.urls = [];
    },
});