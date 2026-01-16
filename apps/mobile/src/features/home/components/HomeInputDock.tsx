import { useState } from 'react';
import { StyleSheet, TextInput, View } from 'react-native';
import { useBottomTabBarHeight } from '@react-navigation/bottom-tabs';

import { HOME_INPUT_DOCK, HOME_SCREEN_COPY } from '@/src/features/home/constants';
import { COLORS } from '@/src/theme/colors';
import { BORDER, LAYOUT, RADIUS, SPACING } from '@/src/theme/layout';
import { TYPOGRAPHY } from '@/src/theme/typography';

export function HomeInputDock() {
  const tabBarHeight = useBottomTabBarHeight();
  const [draftText, setDraftText] = useState('');

  return (
    <View
      style={[
        styles.inputDock,
        { bottom: tabBarHeight + HOME_INPUT_DOCK.marginAboveTabBar },
      ]}
    >
      <TextInput
        value={draftText}
        onChangeText={setDraftText}
        placeholder={HOME_SCREEN_COPY.inputPlaceholder}
        placeholderTextColor={COLORS.textSecondary}
        multiline
        style={styles.textInput}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  inputDock: {
    position: 'absolute',
    left: SPACING.md,
    right: SPACING.md,
  },
  textInput: {
    minHeight: HOME_INPUT_DOCK.minHeight,
    maxHeight: HOME_INPUT_DOCK.maxHeight,
    paddingHorizontal: SPACING.sm,
    paddingVertical: SPACING.sm,
    borderRadius: RADIUS.md,
    borderWidth: BORDER.widthThin,
    borderColor: COLORS.borderSubtle,
    backgroundColor: COLORS.surfaceSubtle,
    fontSize: TYPOGRAPHY.fontSizeBody,
    lineHeight: TYPOGRAPHY.lineHeightBody,
    color: COLORS.textPrimary,
  },
});



