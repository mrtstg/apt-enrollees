<script>
    import { students_list as students, list_empty, group_info, show_group } from './store';
    import { getGroupById } from './InputForm.svelte';
</script>

{#if Object.keys($group_info).length != 0}
    <h1 class="box__header">Группа {$group_info.group_name} </h1>
{:else}
    <h1 class="box__header"> Список абитуриентов </h1>
{/if}

{#if !($list_empty) && $students.length}
    <table class="students_table">
        <tr>
            <th> № </th>
            <th> Имя </th>
            <th> Балл </th>
            {#if $show_group}
                <th> Группа </th>
            {/if}
        </tr>
        {#each $students as student, student_index}
        <tr>
            <td> { student_index + 1} </td>
            <td> { student.name } </td>
            <td> { student.mark } </td>
            {#if $show_group}
                <td> { getGroupById(student.group_id) } </td>
            {/if}
        </tr>
        {/each}
    </table>
{:else if $list_empty}
    <h1 class="box__header pb-0"> На данное направление нет заявок! </h1>
{:else}
    <h1 class="box__header pb-0"> Выберите группу и откройте ее список! </h1>
{/if}
