<script context="module">
    let groups = []
    export function getGroupById(group_id) {
        for (let i = 0; i < groups.length; i++) {
            if (groups[i].id == group_id) {
                return groups[i].name
            }
        }
        return ""
    }
</script>

<script>
    import axios from 'axios';
    import { students_list as students, list_empty, group_info, show_group } from './store';

    async function getGroups() {
        let resp = await axios.get('groups');
        
        try {
            groups = resp.data
            return resp.data
        } catch (error) {
            throw new Error(error)
        }
    }

    async function getStudents() {
        if (selected_group === undefined) {
            alert("Выберите группу!")
            return
        }
        loading_groups = true;
        $show_group = false;
        let resp = await axios.get(
            'students',
            {
                params: {
                    group_id: selected_group
                }
            }
        );
        loading_groups = false;
        try {
            $list_empty = resp.data.students.length === 0
            $students = resp.data.students
            if (resp.data.group_info) {
                $group_info = resp.data.group_info
            } else if ($group_info) {
                $group_info = {}
            }
            if (selected_group === 'all') {
                $show_group = true;
            }
        } catch (error) {
            throw new Error(error)
        }
    }

    let selected_group = undefined;
    let loading_groups = false;
    let promise = getGroups();
</script>

{#await promise}
    <h1 class="box__header"> Загружаем группы... </h1>
{:then}
    <h1 class="box__header"> Выберите группу </h1>
{:catch}
    <h1 class="box__header"> Ошибка! Попробуйте позже. </h1>
{/await}

<select disabled={loading_groups} bind:value={selected_group} class="box__select">
    {#await promise then groups}
        <option disabled> Выберите вариант! </option>
        <option value='all'> Все абитуриенты </option>
        {#each groups as group}
            <option value={group.id}> {group.name} </option>
        {/each}
    {/await}
</select>
{#await promise}
    <button class="button" disabled> Ожидайте... </button>
{:then}
    {#if loading_groups}
        <button class="button" disabled> Ожидайте... </button>
    {:else} 
        <button class="button" on:click={async () => await getStudents()}> Показать список групп </button>
    {/if}
{:catch}
    <button class="button" disabled> Ошибка! </button>
{/await}