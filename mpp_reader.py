import jpype
import mpxj

def read_mpp(file: str) ->list :
    try:
        if not jpype.isJVMStarted():
            jvmPath = jpype.getDefaultJVMPath()
            jpype.startJVM(convertStrings=True)

        if not  jpype.java.lang.Thread.isAttached():
            jpype.attachThreadToJVM()
            jpype.java.lang.Thread.currentThread().\
         setContextClassLoader(jpype.java.lang.ClassLoader.getSystemClassLoader())
        # post process form
    except Exception as e:
        print(e)
    
    from net.sf.mpxj.reader import UniversalProjectReader
    from net.sf.mpxj import FieldTypeClass
    from net.sf.mpxj import TaskField

    project = UniversalProjectReader().read(file)

    # print("Tasks")
    # for task in project.getTasks():
    # 	pd.DataFrame(task)
        # print(task.getID().toString() + "\t" + task.getName() + "\t" + task.getDuration().toString() + "\t" + task.getStart().toString() + "\t" + task.getFinish().toString() + "\t" + task.getPercentageComplete().toString() + "\t");
        # print(task.getActualDuration().toString() + "\t" + task.getRemainingDuration().toString() + "\t" + task.getWork().toString())
        # print(task.getActualWork().toString() + "\t" + task.getRemainingWork().toString() + "\t" + task.getCost().toString() )
        # print(task.getActualCost().toString() + "\t" + task.getRemainingCost().toString() + "\t" + task.getFixedCost().toString() + "\t" + task.getFixedCostAccrual().toString())
        # print(task.getConstraintType().toString() + "\t" + task.getNotes())
        # task.getConstraintType().toString() + "\t" + task.getConstraintDate().toString() + "\t" + task.getConstraintDelay().toString() + "\t" + task.getNotes() + "\t" + task.getOutlineLevel().toString() + "\t" + task.getOutlineNumber().toString())


    # Just to get started, let's see what tasks we have
    # print("Tasks")
    tasks = project.getTasks()

    for task in tasks:
        print(task.getID().toString() + "\t" +
              task.getName())
    print()

    # OK, so what custom field so we have?
    print("Custom Fields")
    for field in project.getCustomFields():
        print(field.getFieldType().getFieldTypeClass().toString() + "\t" +
              field.getFieldType().toString() + "\t" +
              field.getAlias())
    print()

    # Ah! We have custom field definitions here for different entity types
    # (tasks, resources etc). Let's filter that list down to just task custom
    # fields and print those.
    task_custom_fields = list(filter(lambda field: field.getFieldType(
    ).getFieldTypeClass() == FieldTypeClass.TASK, project.getCustomFields()))

    print("Task Custom Fields")
    for field in task_custom_fields:
        print(field.getFieldType().getFieldTypeClass().toString() + "\t" +
              field.getFieldType().toString() + "\t" + field.getAlias())

    # Let's build a report showing the ID, Name and any custom fields for each task.
    # First we'll build a list of column headings and a list of field types
    column_names = ['ID', 'Name']
    column_types = [TaskField.ID, TaskField.NAME]
    for field in task_custom_fields:
        column_names.append(str(field.getAlias()))
        column_types.append(field.getFieldType())

    # Now we can print the column headings, then iterate through the tasks
    # and retrieve the values using the field types.
    # print('\t'.join(column_names))
    count = 0
    dataMPP = []
    result = dict()
    result["count"] = len(tasks)
    for task in tasks:
        data = dict()
        column_values = map(lambda type: str(
            task.getCachedValue(type)), column_types)
        
        # print(task.getID().toString() + "\t" +
        #     task.getName() + "\t" + task.getStart().toString())
        data['id'] =  task.getID().toString()
        data['name'] = task.getName()
        data['duration'] = task.getDuration().toString()
        data['cost'] = task.getCost().toString()
        data['start'] = task.getStart().toString()
        data['finish'] = task.getFinish().toString()
        data['percentageComplete'] = task.getPercentageComplete().toString()
        data['actualDuration'] = task.getActualDuration().toString()
        data['remainingDuration'] = task.getRemainingDuration().toString()
        data['work'] = task.getWork().toString()
        data['actualWork'] = task.getActualWork().toString()
        data['remainingWork'] = task.getRemainingWork().toString()
        data['actualCost'] = task.getActualCost().toString()
        data['remainingCost'] = task.getRemainingCost().toString()
        data['fixedCost'] = task.getFixedCost().toString()
        data['fixedCostAccrual'] = task.getFixedCostAccrual().toString()
        data['constraintType'] = task.getConstraintType().toString()
        data['notes'] = task.getNotes()
        data['outlineLevel'] = task.getOutlineLevel().toString()
        data['outlineNumber'] = task.getOutlineNumber()
        data['wbs'] = task.getWBS()
        data["predecessors"] = task.getPredecessors().toString()
        data["uniqueID"] = task.getUniqueID().toString()
        data["priority"] = task.getPriority().toString()
        data["successors"] = task.getSuccessors().toString()
        dataMPP.append(data)
    result["tasks"] = dataMPP
    return result
    jpype.shutdownJVM()
