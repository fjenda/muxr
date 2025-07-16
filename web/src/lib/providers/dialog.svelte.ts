import type { Component } from "svelte";

export type DialogComponent = Component;
export type DialogProps = Record<string, any>;

export const dialogState = $state({
    component: null as DialogComponent | null,
    props: {} as DialogProps,
    open: false,
});

export const DialogActions = {
    show: (component: DialogComponent, props: DialogProps = {}) => {
        dialogState.component = component;
        dialogState.props = props;
        dialogState.open = true;
    },
    close: () => {
        dialogState.open = false;

        setTimeout(() => {
            dialogState.component = null;
            dialogState.props = {};
        }, 300);
    }
};

if (typeof window !== 'undefined') {
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && dialogState.open) {
            DialogActions.close();
        }
    });
}