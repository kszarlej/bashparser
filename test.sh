ls -l '/'
w
iostat

b=0
echo $b
echo b

c=$(( b+2 ))
echo $c

a=0
if [[ $a == 0 ]];
then
  echo "condition is true";
else
  echo "condition is false";
fi

a=$((a++))
if [[ $a == 0 ]];
then
  echo "condition is true";
else
  echo "condition is false";
fi

iterator=0
while true;
do
  iterator=$(( iterator+1 ))
  if [[ $iterator == 5 ]]; then
    echo "In loop..."
    break;
  fi
done

echo "I just broke out of loop."

iterator=0
while [[ $iterator == 0 ]];
do
  echo "In loop"
  iterator=$((iterator + 1))
done

echo "The loop condition is not true anymore, so stopped looping."

iterator=0
while [[ $iterator <= 5 ]];
do
  iterator=$((iterator++))
  if [[ $iterator <= 4 ]]; then
    continue;
  fi
  echo 'If continue works this line should be printed twice.'
done
