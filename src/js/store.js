import { writable } from "svelte/store";

export const students_list = writable([])
export const group_info = writable({})
export const list_empty = writable(false)
export const show_group = writable(true)
