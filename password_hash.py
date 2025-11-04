def merge_intervals(start_times, end_times):
    # Input validation
    if len(start_times) != len(end_times):
        print("Invalid Input")
        return

    n = len(start_times)

    # Checking for invalid pairs
    invalid_count = 0
    intervals = []
    
    for i in range(n):
        if start_times[i] >= end_times[i]:
            invalid_count += 1
        else:
            intervals.append((start_times[i], end_times[i]))

    # Merge intervals
    if not intervals:
        print("Invalid Input")
        return
    
    # Sort intervals based on start time
    intervals.sort(key=lambda x: x[0])
    
    merged = []
    current_start, current_end = intervals[0]

    for i in range(1, len(intervals)):
        start, end = intervals[i]
        if start <= current_end:  # Overlapping intervals
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end
            
    # Append the last merged interval
    merged.append((current_start, current_end))
    
    # Prepare merged intervals for output
    merged_output = []
    for start, end in merged:
        merged_output.append(start)
        merged_output.append(end)

    print(" ".join(map(str, merged_output)))

    # Count non-overlapping intervals
    non_overlapping_count = 0
    for start, end in intervals:
        if not any(start < other_end and end > other_start for other_start, other_end in merged):
            non_overlapping_count += 1

    print(non_overlapping_count)
    
    # Print invalid pairs count
    print(invalid_count)

# Sample Input
start_times_input = [1, 2, 6, 2, 9, 1]
end_times_input = [0, 1, 8, 5, 10, 3]

# Call the function
merge_intervals(start_times_input, end_times_input)
